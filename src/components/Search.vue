<template>
  <div py-4 />

  <input
    id="input"
    v-model="uid"
    placeholder="Your Email"
    aria-label="Let us Know You!"
    type="email"
    autocomplete="false"
    p="x4 y2"
    w="250px"
    text="center"
    bg="transparent"
    border="~ rounded gray-200 dark:gray-700"
    outline="none active:none"
    @keydown.enter="go"
  />
  <label class="hidden" for="input">Suscribe</label>

  <div>
    <button btn m-3 text-sm :disabled="!uid" @click="go">Go</button>
  </div>
</template>
<script setup lang="ts">
const user = useUserStore();
const uid = $ref(user.savedName);

const router = useRouter();
const go = () => {
  if (uid) router.push(`/auth/${encodeURIComponent(uid)}`);
};
</script>
