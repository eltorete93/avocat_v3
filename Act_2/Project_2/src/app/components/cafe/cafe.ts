import { Injectable } from '@angular/core';

export interface MenuItem {
  id: number;
  name: string;
  description: string;
  price: number;
  category: 'coffee' | 'tea' | 'pastry' | 'sandwich' | 'dessert';
  imageUrl: string;
  available: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class CafeService {
  private menuItems: MenuItem[] = [
    {
      id: 1,
      name: 'Espresso',
      description: 'Rich and bold espresso shot',
      price: 2.50,
      category: 'coffee',
      imageUrl: 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=400',
      available: true
    },
    {
      id: 2,
      name: 'Cappuccino',
      description: 'Espresso with steamed milk and foam',
      price: 3.50,
      category: 'coffee',
      imageUrl: 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400',
      available: true
    },
    {
      id: 3,
      name: 'Latte',
      description: 'Smooth espresso with steamed milk',
      price: 3.75,
      category: 'coffee',
      imageUrl: 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400',
      available: true
    },
    {
      id: 4,
      name: 'Green Tea',
      description: 'Organic green tea leaves',
      price: 2.25,
      category: 'tea',
      imageUrl: 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400',
      available: true
    },
    {
      id: 5,
      name: 'Croissant',
      description: 'Buttery French croissant',
      price: 2.00,
      category: 'pastry',
      imageUrl: 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400',
      available: true
    },
    {
      id: 6,
      name: 'Chocolate Muffin',
      description: 'Rich chocolate chip muffin',
      price: 2.75,
      category: 'pastry',
      imageUrl: 'https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=400',
      available: true
    },
    {
      id: 7,
      name: 'Club Sandwich',
      description: 'Triple-decker with turkey, bacon, and veggies',
      price: 6.50,
      category: 'sandwich',
      imageUrl: 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400',
      available: true
    },
    {
      id: 8,
      name: 'Tiramisu',
      description: 'Classic Italian coffee-flavored dessert',
      price: 4.50,
      category: 'dessert',
      imageUrl: 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400',
      available: true
    },
    {
      id: 9,
      name: 'Mocha',
      description: 'Espresso with chocolate and steamed milk',
      price: 4.00,
      category: 'coffee',
      imageUrl: 'https://images.unsplash.com/photo-1578374173705-22c0fb0f5e06?w=400',
      available: false
    }
  ];

  getMenu(): MenuItem[] {
    return this.menuItems;
  }

  getAvailableMenu(): MenuItem[] {
    return this.menuItems.filter(item => item.available);
  }

  getMenuByCategory(category: string): MenuItem[] {
    return this.menuItems.filter(item => item.category === category && item.available);
  }

  getMenuItem(id: number): MenuItem | undefined {
    return this.menuItems.find(item => item.id === id);
  }
}
