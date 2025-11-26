import { Routes } from '@angular/router';
import { Home } from './components/home/home';
import { CafeHome } from './components/cafe/cafe-home/cafe-home';
import { CafeMenu } from './components/cafe/cafe-menu/cafe-menu';
import { CafeAbout } from './components/cafe/cafe-about/cafe-about';
import { CafeContact } from './components/cafe/cafe-contact/cafe-contact';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'cafeteria', component: CafeHome },
  { path: 'cafe/menu', component: CafeMenu },
  { path: 'cafe/about', component: CafeAbout },
  { path: 'cafe/contact', component: CafeContact },
  { path: '**', redirectTo: '' }
];
