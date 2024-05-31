import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const authToken = authService.getToken();

  // Clonar la solicitud y agregar el encabezado de autorización
  const authReq = req.clone({
    setHeaders: {
      // Authorization: `Bearer ${authToken}`
      Authorization: `Token ${authToken}`      
    }
  });

  // Pasar la solicitud clonada con el encabezado actualizado al siguiente manejador
  return next(authReq);
};