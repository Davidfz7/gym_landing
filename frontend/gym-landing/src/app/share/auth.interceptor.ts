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
      Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NzQwMzEyLCJpYXQiOjE3MTk3MzMxMTIsImp0aSI6IjE0ZjExZjM5ZTZjNTRlNDhhOWEwYjc0MjlhYzRlYjJkIiwidXNlcl9pZCI6M30.lVpruWZHAIAxNuiPem5l9wsr50L7vbVeiDCWAW4wc2Q`
      // Authorization: `Token ${authToken}`      
    }
  });

  // Pasar la solicitud clonada con el encabezado actualizado al siguiente manejador
  return next(authReq);
};