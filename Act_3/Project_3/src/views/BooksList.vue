<template>
  <section class="max-w-7xl mx-auto px-4 py-12">
    <h1 class="text-3xl md:text-4xl font-bold mb-10 text-center">
      {{ booksInfo.tittle }}
    </h1>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-10 text-gray-400 text-xl">
      {{ booksInfo.loadingText }}
    </div>

    <!-- Error -->
    <div v-if="error" class="text-center py-10 text-red-500 text-xl">
      {{ booksInfo.errorText }}
    </div>

    <!-- Categories rendering -->
    <div v-else>
      <div v-for="(books, category) in groupedBooks" :key="category" class="mb-16">

       <!-- Category title -->
        <h2 class="text-2xl md:text-3xl font-semibold mb-6 border-l-4 border-orange-400 pl-3">
          {{ category }}
        </h2>

      <!-- Books grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          <div v-for="book in books" :key="book.id" class="bg-white shadow-md rounded-xl overflow-hidden hover:shadow-xl transition">
            <img :src="book.image" alt="Book cover" class="h-56 w-full object-cover"/>

            <div class="p-4">
              <h3 class="font-semibold text-lg">{{ book.title }}</h3>
              <p class="text-gray-600 text-sm">{{ book.author }}</p>

              <RouterLink :to="`/libro/${book.id}`" class="block mt-3 bg-orange-400 text-black px-4 py-2 rounded-lg text-center font-medium hover:bg-orange-300 transition">
                {{ booksInfo.btnSee }}
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>

const booksInfo = {
  tittle:'Descubre nuestros libros',
  loadingText:'Cargando libros...',
  errorText:'Error al cargar los libros',
  btnSee:'Ver más'

}

import { ref, onMounted, computed } from "vue";

const books = ref([]);
const loading = ref(true);
const error = ref(false);

// 👉 Usamos tu API local en /public
const API_URL = "/public/API.json";

onMounted(async () => {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error("No se pudo cargar");

    const data = await res.json();

    // Aquí sí viene EXACTAMENTE tu estructura
    books.value = data;

  } catch (err) {
    console.error(err);
    error.value = true;
  } finally {
    loading.value = false;
  }
});

// 👉 Agrupar por categoría
const groupedBooks = computed(() => {
  const groups = {};

  books.value.forEach((book) => {
    if (!groups[book.category]) groups[book.category] = [];
    groups[book.category].push(book);
  });

  return groups;
});
</script>
