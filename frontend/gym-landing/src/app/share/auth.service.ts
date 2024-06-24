import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private authUrl = environment.apiURL; 
  private token: string | null = null;

  constructor(private http: HttpClient) {}
  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.authUrl}login/`, { username, password }).pipe(
      tap(response => {
        localStorage.setItem('authToken', response.token);
      })
    );
  }

  getToken(): string | null {
    return localStorage.getItem('authToken');
  }

  isLoggedIn(): boolean {
    return this.getToken() !== null;
  }

  logout(): void {
    localStorage.removeItem('authToken');
  }









  // login(username: string, password: string): Observable<any> {
  //   return this.http.post<any>(`${this.authUrl}/login/`, { username, password }).pipe(
  //     tap(response => this.token = response.token)
  //   );
  // }

  // getToken(): string | null {
  //   return this.token;
  // }

  // isLoggedIn(): boolean {
  //   return this.token !== null;
  // }

  // logout(): void {
  //   this.token = null;
  // }
}
