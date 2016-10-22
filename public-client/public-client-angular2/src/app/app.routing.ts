import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';

const routes: Routes = [
  { path: '', redirectTo: 'sign', pathMatch: 'full' },
  { path: 'about', component: AboutComponent },
  { path: 'sign', component: HomeComponent },
  { path: 'browse', component: HomeComponent},
  { path: 'search', component: HomeComponent}
];

export const routing = RouterModule.forRoot(routes);
