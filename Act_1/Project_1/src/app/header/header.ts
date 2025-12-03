import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  imports: [CommonModule],
  templateUrl: './header.html',
  styleUrl: './header.css',
})
export class Header {

  backgroundImagen = 'assets/images/Background_header3.png';

  logo = 'assets/images/Nexus_logo.png';

  menuBar = {
    home: 'Inicio',
    aboutUs: 'Nosotros',
    blog: 'Blog',
    events: 'Eventos',
    contact: 'Contáctanos'
  }

  categories = {
    book_1:'Infantil',
    book_2:'Juvenil',
    book_3:'Cómic y Manga',
    book_4:'Ciencia Ficción',
    book_5:'No Ficción',
    book_6:'Audiolibros',
    book_7:'Books in English',
    book_8:'Papelería',
    book_9:'eBooks',
    book_10:'Ofertas'
  }

}
