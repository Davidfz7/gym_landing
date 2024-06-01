import { CanActivateFn } from '@angular/router';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { inject } from '@angular/core';

export const authGuard: CanActivateFn = (route, state) => {
    const authService = inject(AuthService);
    const router = inject(Router);
  
      if (authService.isLoggedIn()) {
        return true;
      } else {
        router.navigate(['/productos']);
        return false;
      }
};
