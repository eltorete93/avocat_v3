import { createRouter, createWebHistory } from 'vue-router'

// Imported views

import HeroApp from '@/components/HeroApp.vue'
import AboutUs from '@/views/AboutUs.vue'
import BooksList from '@/views/BooksList.vue'
//import Coworking from '@/views/coworking.vue'
//import cafeteria from '@/views/cafeteria.vue'
import Contact from '@/views/contactApp.vue'
//import Shop from '@/views/shop.vue'

const routes = [
  { path: '/', name: 'home', component: HeroApp},
  { path: '/aboutUs', name: 'aboutUs', component: AboutUs},
  { path: '/books' , name: 'booksList', component: BooksList},
  //{ path: '/coworking', name: 'coworking', component: Coworking},
  //{ path: '/cafeteria', name: 'cafeteria', component: cafeteria},
  { path: '/contact', name: 'contact', component: Contact},
  //{ path: '/shop', name: 'shop', component: Shop}

]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
