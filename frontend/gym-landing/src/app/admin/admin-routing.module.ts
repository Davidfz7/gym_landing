import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminLoginComponent } from './admin-login/admin-login.component';
import { AdminIndexComponent } from './admin-index/admin-index.component';

const routes: Routes = [
  { path:'admin', component: AdminLoginComponent},
  { path:'admin/home', component: AdminIndexComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
