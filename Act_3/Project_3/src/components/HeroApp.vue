<!-- Hero -->

<template>
  <section class="hero-bg relative w-full h-[85vh] md:h-[90vh] bg-cover bg-center bg-no-repeat flex items-center justify-center">
    <!-- Overlay -->
    <div class="absolute inset-0 bg-black/50 animate-fade delay-0"></div>

    <!-- Content -->
    <div class="relative z-10 text-center text-white px-6 max-w-2xl">

      <!-- Títtle -->
      <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 md:mb-6 drop-shadow-lg animate-fadeInUp delay-200 leading-tight">
        {{ heroInfo.tittle }}
      </h1>

      <!-- Subtitle -->
      <p class="text-base sm:text-lg md:text-xl text-gray-200 mb-6 animate-fadeInUp delay-400 px-2">
        {{ heroInfo.subtitle }}
      </p>

      <!-- Button Text -->
      <RouterLink to="/libros" class="bg-orange-400 text-black px-6 sm:px-8 py-3 sm:py-3.5 text-lg sm:text-xl rounded-xl font-semibold hover:bg-orange-300 transition shadow-lg inline-block animate-fadeInUp delay-600" >
        {{ heroInfo.btnText }}
      </RouterLink>

    </div>
  </section>
</template>



<script setup>

const heroInfo ={
  tittle:'Tu espacio para aprender, imaginar y disfrutar',
  subtitle:'Encuentra libros, inspira tu mente y vive la experiencia Nexus.',
  btnText:'Acceder al contenido'
}

</script>





<style scoped>
.hero-bg {
  background-image: url('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f');
}


/* --- Animación fade --- */
@keyframes fade {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animate-fade {
  animation: fade 1.2s ease-in-out forwards;
}

/* --- Fade + movimiento hacia arriba --- */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(25px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeInUp {
  animation: fadeInUp 1.2s ease-out forwards;
}

/* --- Delays escalonados --- */
.delay-0   { animation-delay: 0s; }
.delay-200 { animation-delay: 0.2s; }
.delay-400 { animation-delay: 0.4s; }
.delay-600 { animation-delay: 0.6s; }
</style>
