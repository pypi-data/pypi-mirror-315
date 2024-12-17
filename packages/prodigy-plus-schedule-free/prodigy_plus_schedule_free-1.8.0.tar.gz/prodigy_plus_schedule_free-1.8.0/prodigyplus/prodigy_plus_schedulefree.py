import torch
from .core_optimiser import CoreOptimiser

class ProdigyPlusScheduleFree(CoreOptimiser):
    r"""
    An optimiser based on Prodigy that includes schedule-free logic. Has additional improvements in the form of optional StableAdamW 
    gradient scaling and Adam-atan2 updates, per parameter group adaptation, lower memory utilisation, fused back pass support and 
    tweaks to mitigate uncontrolled LR growth.

    Based on code from:
    https://github.com/facebookresearch/schedule_free
    https://github.com/konstmish/prodigy

    Incorporates improvements from these pull requests (credit to https://github.com/dxqbYD and https://github.com/sangoi-exe):
    https://github.com/konstmish/prodigy/pull/23
    https://github.com/konstmish/prodigy/pull/22
    https://github.com/konstmish/prodigy/pull/20

    As with the reference implementation of schedule-free, a constant scheduler should be used, along with the appropriate
    calls to `train()` and `eval()`. See the schedule-free documentation for more details: https://github.com/facebookresearch/schedule_free
    
    If you do use another scheduler, linear or cosine is preferred, as a restarting scheduler can confuse Prodigy's adaptation logic.

    Leave `lr` set to 1 unless you encounter instability. Do not use with gradient clipping, as this can hamper the
    ability for the optimiser to predict stepsizes. Gradient clipping/normalisation is already handled in the following configurations:
    
    1) `use_stableadamw=True,eps=1e8` (or any reasonable positive epsilon)
    2) `eps=None` (Adam-atan2, scale invariant and can mess with Prodigy's stepsize calculations in some scenarios)

    By default, `split_groups` is set to `True`, so each parameter group will have its own adaptation values. So if you're training
    different networks together, they won't contaminate each other's learning rates. The disadvantage of this approach is that some 
    networks can take a long time to reach a good learning rate when trained alongside others (for example, SDXL's Unet). 
    It's recommended to use a higher `d0` (1e-5, 5e-5, 1e-4) so these networks don't get stuck at a low learning rate.
    
    For Prodigy's reference behaviour, which lumps all parameter groups together, set `split_groups` to `False`.

    In some scenarios, it can be advantageous to freeze Prodigy's adaptive stepsize after a certain number of steps. This
    can be controlled via the `prodigy_steps` settings. This will also free any Prodigy-specific memory used by the
    optimiser (though with all the memory-related improvements, this should not be significant unless you're training
    very large models).

    Arguments:
        params (iterable):
            Iterable of parameters to optimize or dicts defining parameter groups.
        lr (float):
            Learning rate adjustment parameter. Increases or decreases the Prodigy learning rate.
            (default: 1.0)
        betas (Tuple[float, float], optional): 
            Coefficients used for computing running averages of gradient and its square.
            (default: (0.9, 0.99))
        eps (float):
            Term added to the denominator outside of the root operation to improve numerical stability. If set to None,
            Adam-atan2 is used instead. This removes the need for epsilon tuning, but may not work well in all situations.
            (default: 1e-8).
        beta3 (float):
            Coefficient for computing the Prodigy stepsize using running averages. If set to None, uses the value of 
            square root of beta2 
            (default: None).
        weight_decay (float):
            Decoupled weight decay. Use the weight_decay_by_lr setting to determine if decay should be multiplied by the
            adaptive learning rate.
            (default: 0).
        weight_decay_by_lr (boolean):
            If True, weight_decay is multiplied by the adaptive learning rate (as per the PyTorch implementation of AdamW).
            If False, weight_decay will have a much stronger effect.
            (default: True).
        use_bias_correction (boolean):
            Turn on Adafactor-style bias correction, which scales beta2 directly. (default: False).
        d0 (float):
            Initial estimate for Prodigy. Also serves as the minimum learning rate.
            (default: 1e-6).
        d_coef (float):
            Coefficient in the expression for the estimate of d. Values such as 0.5 and 2.0 typically work as well. 
            Changing this parameter is the preferred way to tune the method.
            (default: 1.0)
        prodigy_steps (int):
            Freeze Prodigy stepsize adjustments after a certain optimiser step and releases all state memory required
            by Prodigy.
            (default: 0)
        split_groups (boolean):
            Track individual adaptation values for each parameter group. For example, if training
            a text encoder beside a Unet. Note this can have a significant impact on training dynamics.
            Set to False for original Prodigy behaviour, where all groups share the same values.
            (default: True)
        split_groups_mean (boolean):
            When split_groups is True, use the harmonic mean of learning rates for all groups. This favours
            a more conservative LR. Calculation remains per-group. If split_groups is False, this value has no effect.
            Set to False to have each group use its own learning rate. 
            (default: True)
        factored (boolean):
            Use factored approximation of the second moment, similar to Adafactor. Reduces memory usage. Disable
            if training results in NaNs or the learning rate fails to grow.
            (default: True)
        fused_back_pass (boolean):
            Stops the optimiser from running the normal step method. Set to True if using fused backward pass.
            (default: False)
        use_stableadamw (boolean):
            Scales parameter updates by the root-mean-square of the normalised gradient, in essence identical to 
            Adafactor's gradient scaling. Set to False if the adaptive learning rate never improves.
            (default: True)
        use_muon_pp (boolean):
            Experimental. Perform orthogonalisation on the gradient before it is used for updates ala Shampoo/SOAP/Muon.
            (https://github.com/KellerJordan/Muon/blob/master/muon.py). Not suitable for all training scenarios.
            May not work well with small batch sizes or finetuning.
            (default: False)
        use_cautious (boolean):
            Experimental. Perform "cautious" updates, as proposed in https://arxiv.org/pdf/2411.16085. Modifies
            the update to isolate and boost values that align with the current gradient. Note that we do not have
            access to a first moment, so this deviates from the paper (we apply the mask directly to the update).
            May have a limited effect.
            (default: False)
        use_adopt (boolean):
            Experimental. Performs a modified step where the second moment is updated after the parameter update,
            so as not to include the current gradient in the denominator. This is a partial implementation of ADOPT 
            (https://arxiv.org/abs/2411.02853), as we don't have a first moment to use for the update.
            (default: False)
        stochastic_rounding (boolean):
            Use stochastic rounding for bfloat16 weights (https://github.com/pytorch/pytorch/issues/120376). Brings
            bfloat16 training performance close to that of float32.
            (default: True)
    """
    def __init__(self, params, lr=1.0,
                 betas=(0.9, 0.99), beta3=None,
                 weight_decay=0.0,
                 weight_decay_by_lr=True,
                 use_bias_correction=False,
                 d0=1e-6, d_coef=1.0,
                 prodigy_steps=0,
                 eps=1e-8,
                 split_groups=True,
                 split_groups_mean=True,
                 factored=True,
                 fused_back_pass=False,
                 use_stableadamw=True,
                 use_muon_pp=False,
                 use_cautious=False,
                 use_adopt=False,
                 stochastic_rounding=True):
        
        super().__init__(params=params, lr=lr, betas=betas, beta3=beta3,
                         weight_decay=weight_decay, weight_decay_by_lr=weight_decay_by_lr,
                         use_bias_correction=use_bias_correction,
                         d0=d0, d_coef=d_coef, prodigy_steps=prodigy_steps,
                         eps=eps, split_groups=split_groups,
                         split_groups_mean=split_groups_mean, factored=factored,
                         fused_back_pass=fused_back_pass, use_stableadamw=use_stableadamw,
                         use_muon_pp=use_muon_pp, use_cautious=use_cautious, use_adopt=use_adopt,
                         stochastic_rounding=stochastic_rounding)

    @torch.no_grad()
    def eval(self):
        for group in self.param_groups:
            if not group['train_mode']:
                continue
            beta1, _ = group['betas']
            for p in group['params']:
                z = self.state[p].get('z')
                if z is not None:
                    # Set p to x
                    p.lerp_(end=z.to(device=p.device), weight=1 - 1 / beta1)
            group['train_mode'] = False

    @torch.no_grad()
    def train(self):
        for group in self.param_groups:
            if group['train_mode']:
                continue
            beta1, _ = group['betas']
            for p in group['params']:
                z = self.state[p].get('z')
                if z is not None:
                    # Set p to y
                    p.lerp_(end=z.to(device=p.device), weight=1 - beta1)
            group['train_mode'] = True

    @torch.no_grad()
    def initialise_state(self, p, group):
        state, needs_init = self.initialise_state_internal(p, group)

        if needs_init:
            state['z'] = p.detach().clone(memory_format=torch.preserve_format)
        
        return state
    
    @torch.no_grad()
    def update_params(self, y, z, update, group):
        dlr = self.get_dlr(group)
        decay = group['weight_decay']
        beta1, _ = group['betas']

        weight = self.get_d_max(group) ** 2
        weight_sum = group['weight_sum'] + weight
        ckp1 = weight / weight_sum if weight_sum else 0

        y.lerp_(end=z, weight=ckp1)

        # Weight decay at Y.
        if decay != 0:
            if group['weight_decay_by_lr']:
                decay *= dlr
            y.sub_(y, alpha=decay * (1 - beta1))
            z.sub_(y, alpha=decay)

        y.add_(update, alpha=dlr * (beta1 * (1 - ckp1) - 1))
        z.sub_(update, alpha=dlr)

        return weight_sum

    @torch.no_grad()
    def step_param(self, p, group):
        if not group['train_mode']:
            raise Exception("Not in train mode!")

        self.on_start_step(group)

        weight_sum = group['weight_sum']
        
        if p.grad is not None:
            grad = p.grad.float()
            grad_mask = grad.clone() if group['use_cautious'] else None
            rms_min = 1.0 if group['use_stableadamw'] else None

            state = self.initialise_state(p, group)
            y, z = p, state['z']

            self.update_prodigy(state, group, grad, z)
            update = None
            
            if state['muon']:
                rms_min = 1e-7
                # Use high epsilon at start of training so
                # Prodigy doesn't take forever to adapt the stepsize.
                eps = max(rms_min, 0.2 ** group['k'] ** 0.5)
                update = self.newton_schulz_(grad, eps=eps)
            else:
                use_adopt = group['use_adopt']

                if use_adopt and group['k'] == 1:
                    self.update_second_moment(state, group, grad, 0, return_denom=False)
                else:
                    _, beta2 = group['betas']
                    denom = self.update_second_moment(state, group, grad, beta2, denom_before_update=use_adopt)
                    update = self.update_(grad, denom, group)
                    del denom

            if update is not None:
                if rms_min is not None:
                    self.rms_(update, rms_min)

                if grad_mask is not None:
                    self.cautious_(update, grad_mask)
                    del grad_mask

                if group['stochastic_rounding'] and y.dtype == z.dtype == torch.bfloat16:
                    y_fp32, z_fp32 = y.float(), z.float()

                    weight_sum = self.update_params(y_fp32, z_fp32, update, group)

                    self.copy_stochastic_(y, y_fp32)
                    self.copy_stochastic_(z, z_fp32)

                    del y_fp32, z_fp32
                else:
                    weight_sum = self.update_params(y, z, update, group)

                del update

        if self.on_end_step(group):
            group['weight_sum'] = weight_sum