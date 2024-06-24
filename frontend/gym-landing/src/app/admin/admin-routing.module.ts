import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminLoginComponent } from './admin-login/admin-login.component';
import { AdminIndexComponent } from './admin-index/admin-index.component';
import { AdminProductoComponent } from './admin-producto/admin-producto.component';
import { AdminCostumerComponent } from './admin-costumer/admin-costumer.component';
import { AdminSalesComponent } from './admin-sales/admin-sales.component';

const routes: Routes = [
  { path:'admin', component: AdminLoginComponent},
  { path:'admin/inicio', component: AdminIndexComponent},
  { path:'admin/productos', component: AdminProductoComponent},
  { path:'admin/compradores', component: AdminCostumerComponent},
  { path:'admin/ventas', component: AdminSalesComponent},
  // { path:'admin/analytics', component: AdminIndexComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
