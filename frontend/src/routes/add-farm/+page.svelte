<script lang="ts">
    let farm_key = "";
    function register_fk(){
        alert(`fk: ${farm_key}`);
    }
</script>
<div class="flex align-center justify-center">
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <div class="form-control">
          <label class="label">
            <span class="label-text">Enter The Key of the farm</span>
          </label>
          <input type="text" class="input input-bordered" bind:value={farm_key}/>
        </div>
        <div class="form-control mt-5">
          <button class="btn btn-secondary white" on:click={register_fk}>Enter</button>
        </div>
        <div class="form-control mt-5">
            <a href="/" class="btn btn-primary white">Cancel</a>
        </div>
      </div>
  </div>
</div>