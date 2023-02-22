<script>
    import Nav from "$lib/Nav.svelte";
    import "./app.css"
</script>
<Nav/>
<slot></slot>
<style>
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
</style>