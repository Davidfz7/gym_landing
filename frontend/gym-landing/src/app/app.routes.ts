import { Routes } from '@angular/router';
import { ProductoIndexComponent } from './producto/producto-index/producto-index.component';
import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component';
import { InicioComponent } from './home/inicio/inicio.component';
import { AdminLoginComponent } from './admin/admin-login/admin-login.component';
import { AdminIndexComponent } from './admin/admin-index/admin-index.component';

export const routes: Routes = [
    { path:'productos', component: ProductoIndexComponent},
    { path:'inicio', component: InicioComponent},

    { path:'admin', component: AdminLoginComponent},
    { path:'admin/home', component: AdminIndexComponent},

    { path:'', redirectTo:'/inicio' ,pathMatch:'full'},
    { path:'**',component:PageNotFoundComponent},
];
