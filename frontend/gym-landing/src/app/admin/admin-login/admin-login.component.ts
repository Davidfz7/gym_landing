import { Component } from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {FormControl, FormGroupDirective, NgForm, Validators, FormsModule, ReactiveFormsModule,} from '@angular/forms';
import {MatIconModule} from '@angular/material/icon';
import {ErrorStateMatcher} from '@angular/material/core';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import { FormBuilder, FormGroup } from '@angular/forms';
import { AuthService } from '../../share/auth.service';

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}


@Component({
  selector: 'app-admin-login',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, FormsModule, MatFormFieldModule, MatInputModule, ReactiveFormsModule, MatIconModule],
  templateUrl: './admin-login.component.html',
  styleUrl: './admin-login.component.scss'
})

export class AdminLoginComponent {
  // emailFormControl = new FormControl('', [Validators.required, Validators.email]);
  matcher = new MyErrorStateMatcher();
  value = '';
  value2 = '';
  loginForm: FormGroup;

  

  correo='';

  constructor(private fb: FormBuilder, private authService: AuthService) {
    this.loginForm = this.fb.group({
      email: [Validators.required],
      password: [Validators.required],
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      const email = this.loginForm.get('email').value;
      const password = this.loginForm.get('password').value;
      this.authService.login(email, password).subscribe(response => {
        if (this.authService.isLoggedIn()) {
          console.log('Login successful');
          console.log(Date.now)
        } else {
          console.log('Login failed');
        }
      });
    }
  }


  // login(): void {
  //   this.authService.login(this.correo).subscribe(response => {
  //     if (this.authService.isLoggedIn()) {
  //       console.log('Login successful');
  //       // Redirigir al usuario o hacer otra cosa
  //     } else {
  //       console.log('Login failed');
  //     }
  //   });
  // }

  logout(): void {
    this.authService.logout();
    console.log('Logged out');
  }

}
