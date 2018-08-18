<template>
  <div class="container">
      <div class="jumbotron">
          <h1>Hello World!</h1>
      </div>
      <HelloWorld/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'home',
  components: {
    HelloWorld
  }
}
</script>
