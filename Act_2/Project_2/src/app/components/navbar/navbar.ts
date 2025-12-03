import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css'],
})

export class Navbar {

  brandName = {
    name:'Nexus',
    descriptor: 'Book'
  };

  menuBar = {
    home:'Inicio',
    books:'Libros',
    aboutUs:'Sobre nosotros',
    categories:'Categorias',
    subCategories_1:{
      fiction:'Ficción',
      nonFiction:'No Ficción',
      science:'Ciencia',
      history:'Historia'
    },
    coworking:'Coworking',
    subCategories_2:{
      plans:'Planes y precios',
      reservations:'Reservas',
      services:'Servicios',
      memberships:'Membresías'
    },
    contact:'Contacto',
    purchase:'Comprar',
    login: 'Iniciar Sesión',
    coffeeShop: 'Cafetería'
  };

}
