import { Routes } from '@angular/router';
import { ProductoIndexComponent } from './producto/producto-index/producto-index.component';
import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component';
import { InicioComponent } from './home/inicio/inicio.component';

export const routes: Routes = [
    { path:'productos', component: ProductoIndexComponent},
    { path:'inicio', component: InicioComponent},

    { path:'', redirectTo:'/inicio' ,pathMatch:'full'},
    { path:'**',component:PageNotFoundComponent},
];
