<template>
  <div class="page-header-wrapper">
    <v-card 
      elevation="0"
      class="rounded-b-2xl overflow-hidden page-header-card"
      style="background: linear-gradient(135deg, #2E7D32 0%, #1976D2 100%); color: white;"
    >
      <v-card-text class="pa-6 py-8">
        <v-row align="center" justify="space-between">
          <v-col cols="auto" class="d-flex align-center gap-4">
            <v-btn
              icon
              size="large"
              color="white"
              variant="text"
              @click="goBack"
              class="hover:bg-white hover:bg-opacity-20 transition-all"
            >
              <v-icon size="32">mdi-arrow-left</v-icon>
            </v-btn>
            <div>
              <h1 class="text-h4 font-weight-bold text-white mb-0" style="letter-spacing: -0.5px;">
                {{ title }}
              </h1>
              <p v-if="subtitle" class="text-subtitle-2 text-white opacity-90 mb-0 mt-1">
                {{ subtitle }}
              </p>
            </div>
          </v-col>
          <v-col cols="auto" class="d-flex gap-2">
            <slot name="actions"></slot>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  }
})

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.page-header-wrapper {
  margin-bottom: 24px;
}

.page-header-card {
  box-shadow: 0 10px 30px rgba(46, 125, 50, 0.15);
}

.gap-4 {
  gap: 16px;
}

.gap-2 {
  gap: 8px;
}

.d-flex {
  display: flex;
}

.align-center {
  align-items: center;
}

.justify-space-between {
  justify-content: space-between;
}
</style>
