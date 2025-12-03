import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BookCatalog } from './book-catalog';

describe('BookCatalog', () => {
  let component: BookCatalog;
  let fixture: ComponentFixture<BookCatalog>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BookCatalog]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BookCatalog);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
