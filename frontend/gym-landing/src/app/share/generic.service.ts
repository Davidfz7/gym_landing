import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment'; 


@Injectable({
  providedIn: 'root'
})
export class GenericService {

  // URL del API, definida en enviroments->enviroment.ts
  urlAPI: string = environment.apiURL;
  //Información usuario actual
  currentUser: any;


  constructor(private http: HttpClient) { 

  }

  // Listar
  list(endopoint: string): Observable<any> {
    return this.http.get<any>(this.urlAPI + endopoint);
  }

   create(endopoint: string, objCreate: any | any): Observable<any | any[]> {
    return this.http.post<any | any[]>(this.urlAPI + endopoint, objCreate);
  }


  // // Obtener
  // get(endopoint: string, filtro: any): Observable<any | any[]> {
  //   return this.http.get<any | any[]>(this.urlAPI + endopoint + `/${filtro}`);
  // }
  // // crear
  // create(endopoint: string, objCreate: any | any): Observable<any | any[]> {
  //   return this.http.post<any | any[]>(this.urlAPI + endopoint, objCreate);
  // }
  // // actualizar
  // update(endopoint: string, objUpdate: any | any): Observable<any | any[]> {
  //   return this.http.put<any | any[]>(
  //     this.urlAPI + endopoint + `/${objUpdate.id}`,
  //     objUpdate
  //   );
  // }
  // // borrar
  // delete(endopoint: string, filtro: any | any): Observable<any | any[]> {
  //   return this.http.delete<any | any[]>(this.urlAPI + endopoint + `/${filtro}`);
  // }


}
