<template>
  <div :class="[
    'bg-white p-8 rounded-xl shadow-lg',
    isPopular ? 'border-2 border-blue-600 transform scale-105' : ''
  ]">
    <h3 class="text-xl font-semibold mb-4">{{ name }}</h3>
    <p class="text-4xl font-bold mb-6">
      {{ price ? `$${price}` : priceLabel }}<span v-if="price" class="text-lg text-gray-500">/mo</span>
    </p>
    <ul class="space-y-3 mb-8">
      <li v-for="feature in features" :key="feature" class="flex items-center">
        <svg class="h-5 w-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        {{ feature }}
      </li>
    </ul>
    <button class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">
      {{ price ? 'Get Started' : 'Contact Sales' }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  name: String,
  price: Number,
  priceLabel: String,
  features: Array,
  isPopular: Boolean
})
</script>