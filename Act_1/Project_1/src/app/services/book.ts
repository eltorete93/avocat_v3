import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable,map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class Book {
  private apiUrl = 'https://gutendex.com/books';

  constructor(private http: HttpClient) {}

getBooks(): Observable<any[]> {
    return this.http.get<any>(this.apiUrl).pipe(
      map(response =>
        response.results.slice(0, 4).map((book: any) => ({
          title: book.title,
          description: book.authors && book.authors.length > 0
            ? 'Autor: ' + book.authors[0].name
            : 'Autor desconocido',
          image: book.formats['image/jpeg'] || 'https://via.placeholder.com/200x300?text=No+Image',
          link: book.formats['text/html'] || `https://gutendex.com/books/${book.id}`
        }))
      )
    );
  }

}
