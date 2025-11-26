import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BooksService } from '../../Services/books-service';
import { Book } from '../books/books';

@Component({
  selector: 'app-new-releases',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './new-releases.html',
  styleUrls: ['./new-releases.css'],
})
export class NewReleases implements OnInit {

  latestBooks = {
    mainTittle:'Próximos Lanzamientos'
  };

  upcomingBooks: Book[] =  [];

  constructor(private booksService : BooksService) {}

  ngOnInit(): void {
    this.loadUpcomingBooks();
  }

loadUpcomingBooks(): void {
  this.booksService.getUpcomingBooks().subscribe({
    next: (data: Book[]) => {
      this.upcomingBooks = data;
    },
    error: (err) => {
      console.error('Error al cargar libros', err);
    }
  });
}


}
