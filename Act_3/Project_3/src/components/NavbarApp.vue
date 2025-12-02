<!-- NavBar -->

<template>
  <nav class="bg-[#2c414f] text-white shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Logo -->
        <div class="flex items-center space-x-3">
          <img src="../assets/nexus_logo.png" alt="Nexus Logo" class="h-10 w-auto" />
          <span class="text-xl font-semibold">Nexus</span>
        </div>

        <!-- MENU PARA ESCRITORIO -->
        <div class="hidden md:flex space-x-6 text-lg ml-auto mr-6">
          <RouterLink to="/" class="hover:text-orange-300">Inicio</RouterLink>
          <RouterLink to="/books" class="hover:text-orange-300">Libros</RouterLink>
          <RouterLink to="/aboutUs" class="hover:text-orange-300">Sobre nosotros</RouterLink>
          <RouterLink to="/coworking" class="hover:text-orange-300">Coworking</RouterLink>
          <RouterLink to="/cafeteria" class="hover:text-orange-300">Cafeteria</RouterLink>
          <RouterLink to="/contact" class="hover:text-orange-300">Contacto</RouterLink>
          <RouterLink to="/shop" class="hover:text-orange-300"><ShoppingCartIcon class="h-6 w-6"/></RouterLink>
        </div>

        <!-- BOTÓN LOGIN (ESCRITORIO) -->
        <div class="hidden md:flex">
          <RouterLink to="/login" class="bg-orange-400 text-black px-4 py-2 rounded-lg font-medium hover:bg-orange-300 transition">
            Login
          </RouterLink>
        </div>

        <!-- BOTÓN HAMBURGUESA (MÓVIL) -->
        <button @click="isOpen = !isOpen" class="md:hidden text-white focus:outline-none text-3xl">
          ☰
        </button>
      </div>
    </div>

    <!-- MENÚ MÓVIL -->
    <div v-if="isOpen" class="md:hidden bg-[#2c414f] px-4 pb-4 space-y-3 text-lg">
      <RouterLink class="block hover:text-orange-300" to="/">Inicio</RouterLink>
      <RouterLink class="block hover:text-orange-300" to="/libros">Libros</RouterLink>
      <RouterLink class="block hover:text-orange-300" to="/sobre-nosotros"
        >Sobre nosotros</RouterLink
      >
      <RouterLink class="block hover:text-orange-300" to="/categorias">Categorías</RouterLink>
      <RouterLink class="block hover:text-orange-300" to="/coworking">Coworking</RouterLink>
      <RouterLink class="block hover:text-orange-300" to="/contacto">Contacto</RouterLink>
      <RouterLink class="block hover:text-orange-300" to="/carrito"
        ><ShoppingCartIcon class="h-6 w-6"
      /></RouterLink>

      <RouterLink
        to="/login"
        class="block bg-orange-400 text-black px-4 py-2 rounded-lg font-medium hover:bg-orange-300 transition"
      >
        Login
      </RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { ShoppingCartIcon } from '@heroicons/vue/24/outline'

const isOpen = ref(false)
</script>
