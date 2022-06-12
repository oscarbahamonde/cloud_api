<script setup lang="ts">
const props = defineProps<{ uid: string }>()
const router = useRouter()
const user = useUserStore()
watchEffect(() => {
  user.setNewName(props.uid)
})
</script>

<template>
  <div>
    <div text-4xl>
      <div i-carbon-pedestrian inline-block />
    </div>
    <p>
      {{ props.uid }}
    </p>
    <template v-if="user.otherNames.length">
      <p text-sm mt-4>
        <span opacity-75>AKA as</span>
        <ul>
          <li v-for="otherName in user.otherNames" :key="otherName">
            <router-link :to="`/hi/${otherName}`" replace>
              {{ otherName }}
            </router-link>
          </li>
        </ul>
      </p>
    </template>

    <div>
      <button
        btn m="3 t6" text-sm
        @click="router.back()"
      >
        Atrás
      </button>
    </div>
  </div>
</template>
