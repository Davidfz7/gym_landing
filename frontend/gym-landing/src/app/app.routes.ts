import { Routes } from '@angular/router';
import { ProductoIndexComponent } from './producto/producto-index/producto-index.component';
import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component';
import { InicioComponent } from './home/inicio/inicio.component';
import { AdminLoginComponent } from './admin/admin-login/admin-login.component';
import { AdminIndexComponent } from './admin/admin-index/admin-index.component';
import { AvisosIndexComponent } from './avisos/avisos-index/avisos-index.component';
import { CanActivateFn } from '@angular/router';
import { authGuard } from './share/guards/auth.guard';

export const routes: Routes = [
    { path:'productos', component: ProductoIndexComponent},
    { path:'inicio', component: InicioComponent},

    { path:'avisos', component: AvisosIndexComponent},

    { path:'admin', component: AdminLoginComponent},
    { path:'admin/home', component: AdminIndexComponent, canActivate: [authGuard]},

    // {
    //     path: 'admin/home',
    //     canActivate: [authGuard],
    // },

    { path:'', redirectTo:'/inicio' ,pathMatch:'full'},
    { path:'**',component:PageNotFoundComponent},
];
