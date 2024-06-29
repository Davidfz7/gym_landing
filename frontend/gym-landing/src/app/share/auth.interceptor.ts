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
      Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NzA3OTI0LCJpYXQiOjE3MTk3MDA3MjQsImp0aSI6ImE1ZjY5Yzk0MzA1NTRmOTc4ZTY1ZmE3Y2EzMTcyY2YwIiwidXNlcl9pZCI6M30.CKMgN87ZCIS6xvYADD9qBpfOI_jVCciOHCURDrQCAMU`
      // Authorization: `Token ${authToken}`      
    }
  });

  // Pasar la solicitud clonada con el encabezado actualizado al siguiente manejador
  return next(authReq);
};