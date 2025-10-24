import { Component,OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Book } from '../services/book';


@Component({
  selector: 'app-book-catalog',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './book-catalog.html',
  styleUrl: './book-catalog.css',
})

export class BookCatalog implements OnInit {

  books: any[] = [];


  constructor(private book: Book) {}

ngOnInit(): void {
    this.book.getBooks().subscribe((data) => {
      this.books = data;
    });
  }
}



