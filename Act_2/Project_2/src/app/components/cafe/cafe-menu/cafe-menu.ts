import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CafeService, MenuItem } from '../cafe';

@Component({
  selector: 'app-cafe-menu',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cafe-menu.html',
  styleUrls: ['./cafe-menu.css'],
})
export class CafeMenu implements OnInit {
  menuItems: MenuItem[] = [];
  selectedCategory: string = 'all';
  categories = [
    { value: 'all', label: 'All Items' },
    { value: 'coffee', label: 'Coffee' },
    { value: 'tea', label: 'Tea' },
    { value: 'pastry', label: 'Pastries' },
    { value: 'sandwich', label: 'Sandwiches' },
    { value: 'dessert', label: 'Desserts' }
  ];

  constructor(private cafeService: CafeService) {}

  ngOnInit(): void {
    this.loadMenu();
  }

  loadMenu(): void {
    this.menuItems = this.cafeService.getAvailableMenu();
  }

  filterByCategory(category: string): void {
    this.selectedCategory = category;
    if (category === 'all') {
      this.menuItems = this.cafeService.getAvailableMenu();
    } else {
      this.menuItems = this.cafeService.getMenuByCategory(category);
    }
  }

  getCategoryBadgeClass(category: string): string {
    const badges: {[key: string]: string} = {
      'coffee': 'bg-warning',
      'tea': 'bg-success',
      'pastry': 'bg-info',
      'sandwich': 'bg-danger',
      'dessert': 'bg-primary'
    };
    return badges[category] || 'bg-secondary';
  }
}
