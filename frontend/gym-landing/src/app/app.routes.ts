import { Routes } from '@angular/router';
import { ProductoIndexComponent } from './producto/producto-index/producto-index.component';
import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component';
import { InicioComponent } from './home/inicio/inicio.component';
import { AdminLoginComponent } from './admin/admin-login/admin-login.component';
import { AdminIndexComponent } from './admin/admin-index/admin-index.component';
import { AvisosIndexComponent } from './avisos/avisos-index/avisos-index.component';
import { CanActivateFn } from '@angular/router';
import { authGuard } from './share/guards/auth.guard';
import { ProductoPesasComponent } from './producto/producto-pesas/producto-pesas.component';
import { ProductoEquiposComponent } from './producto/producto-equipos/producto-equipos.component';
import { ProductoMaquinasComponent } from './producto/producto-maquinas/producto-maquinas.component';
import { ProductoDetailComponent } from './producto/producto-detail/producto-detail.component';
import { ProductoHomeComponent } from './producto/producto-home/producto-home.component';

export const routes: Routes = [
    { path:'productos', component: ProductoIndexComponent},
    { path:'productos/home', component: ProductoHomeComponent},
    { path:'productos/pesas', component: ProductoPesasComponent},
    { path:'productos/equipos', component: ProductoEquiposComponent},
    { path:'productos/maquinas', component: ProductoMaquinasComponent},
    { path: 'product/:id', component: ProductoDetailComponent },


    { path:'inicio', component: InicioComponent},

    { path:'avisos', component: AvisosIndexComponent},

    { path:'admin', component: AdminLoginComponent},
    { path:'admin/home', component: AdminIndexComponent, canActivate: [authGuard]},


    { path:'', redirectTo:'/productos' ,pathMatch:'full'},
    { path:'**',component:PageNotFoundComponent},
];
