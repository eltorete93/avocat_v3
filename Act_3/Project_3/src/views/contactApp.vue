<template>
  <section class="bg-gray-100 py-12 px-6">
    <div class="max-w-3xl mx-auto bg-white shadow-lg rounded-2xl p-8">

      <!-- Título -->
      <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">
        Contáctanos
      </h2>

      <!-- Descripción -->
      <p class="text-center text-gray-600 mb-10">
        ¿Tienes dudas sobre nuestra librería, coworking o cafetería?
        Envíanos un mensaje y te responderemos muy pronto.
      </p>

      <!-- Formulario -->
      <form @submit.prevent="handleSubmit" class="space-y-6">

        <!-- Nombre -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
          <input
            v-model="form.name"
            type="text"
            class="w-full p-3 border rounded-lg focus:ring focus:ring-orange-300"
            placeholder="Tu nombre"
            required
          />
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="w-full p-3 border rounded-lg focus:ring focus:ring-orange-300"
            placeholder="tucorreo@example.com"
            required
          />
        </div>

        <!-- Mensaje -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Mensaje</label>
          <textarea
            v-model="form.message"
            rows="4"
            class="w-full p-3 border rounded-lg focus:ring focus:ring-orange-300"
            placeholder="Escribe tu mensaje aquí..."
            required
          ></textarea>
        </div>

        <!-- Botón -->
        <button
          type="submit"
          class="w-full bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-lg transition font-semibold"
        >
          Enviar mensaje
        </button>
      </form>

      <!-- Mensaje de éxito -->
      <p
        v-if="success"
        class="mt-6 text-green-600 font-semibold text-center"
      >
        ¡Mensaje enviado con éxito! 🎉
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";

const form = ref({
  name: "",
  email: "",
  message: "",
});

const success = ref(false);

const handleSubmit = () => {
  console.log("Formulario enviado:", form.value);

  // Aquí puedes integrar EmailJS, una API, o backend
  success.value = true;

  // Limpiar formulario
  form.value = { name: "", email: "", message: "" };

  setTimeout(() => (success.value = false), 4000);
};
</script>
