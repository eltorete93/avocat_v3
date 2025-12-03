<!-- AboutUs -->

<template>
  <section ref="sectionRef" :class="['bg-[#f4f4f4] py-16 px-6 transition-all duration-700 ease-out', isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10']">
    <div class="max-w-7xl mx-auto">

      <!-- Títtle -->
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-[#2c414f]">{{ aboutUsData.title }}</h2>
        <p class="text-lg mt-3 text-gray-600">{{ aboutUsData.subtititle }}</p>
      </div>

      <div class="grid md:grid-cols-2 gap-12 items-center">

        <!-- Imagen -->
        <div class="rounded-xl overflow-hidden shadow-lg transform transition hover:-translate-y-1">
          <img src="../assets/ChatGPT Image Nov 30, 2025, 09_40_28 PM.png" alt="Nexus" class="w-full h-96 object-cover"/>
        </div>

        <!-- Text -->
        <div class="space-y-6 text-gray-700 leading-relaxed">

          <p>
            En <span class="font-semibold text-[#2c414f]">{{ aboutUsData.title }}</span> creemos que cada historia,
            cada idea y cada taza de café puede conectar personas. Creamos un
            espacio donde lectores, estudiantes y emprendedores pueden crecer.
          </p>

          <p>
            Nuestra librería ofrece un catálogo seleccionado cuidadosamente.
            Además contamos con un área de
            <span class="font-semibold text-[#2c414f]">coworking moderno</span>
            y una
            <span class="font-semibold text-[#2c414f]">cafetería artesanal</span>
            para acompañar tus momentos favoritos.
          </p>

          <!-- Icons -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center pt-4">

            <div class="bg-white p-5 rounded-xl shadow-md hover:shadow-lg transition">
              <BookOpenIcon class="mx-auto w-10 h-10 text-[#2c414f]" />
              <h4 class="font-semibold mt-3">{{ aboutUsData.books }}</h4>
              <p class="text-sm text-gray-500">{{ aboutUsData.subtittleBooks }}</p>
            </div>

            <div class="bg-white p-5 rounded-xl shadow-md hover:shadow-lg transition">
              <ComputerDesktopIcon class="mx-auto w-10 h-10 text-[#2c414f]" />
              <h4 class="font-semibold mt-3">{{ aboutUsData.coworking }}</h4>
              <p class="text-sm text-gray-500">{{ aboutUsData.subtititleCoworking }}</p>
            </div>

            <div class="bg-white p-5 rounded-xl shadow-md hover:shadow-lg transition">
              <BeakerIcon class="mx-auto w-10 h-10 text-[#2c414f]" />
              <h4 class="font-semibold mt-3">{{ aboutUsData.cafeteria }}</h4>
              <p class="text-sm text-gray-500">{{ aboutUsData.subtititleCafeteria }}</p>
            </div>

          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup>

const aboutUsData ={
  title: "Nexus",
  subtititle:"Un espacio donde los libros, la creatividad y el café se encuentran",
  books:"Librería",
  subtittleBooks:"Títulos para todos los gustos",
  coworking:"Coworking",
  subtititleCoworking:"Espacio moderno y colaborativo",
  cafeteria:"Cafetería",
  subtititleCafeteria:"Café fresco y ambiente acogedor"

}

import { ref, onMounted } from "vue";
import {
  BookOpenIcon,
  ComputerDesktopIcon,
  BeakerIcon,
} from "@heroicons/vue/24/outline";

// Referencia de la sección
const sectionRef = ref(null);
const isVisible = ref(false);

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          isVisible.value = true;
          observer.disconnect();
        }
      });
    },
    { threshold: 0.2 }
  );

  observer.observe(sectionRef.value);
});
</script>
