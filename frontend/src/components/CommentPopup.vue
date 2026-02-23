<script>
export default {
  props: {
    visible: Boolean,
    modelValue: String
  },
  emits: [
    "update:modelValue",
    "save",
    "cancel"
  ],
};
</script>

<template>
          <!-- Kommentar Popup -->
    <div v-if="visible" class="comment-popup">
      <textarea :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" placeholder="Kommentar eingeben..." rows="4"></textarea>
      <div class="comment-popup-buttons">
        <button @click="$emit('cancel')">Abbrechen</button>
        <button @click="$emit('save')">Speichern</button>
      </div>
    </div>
</template>

<style scoped>
.comment-popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  background: white;
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  z-index: 1000;
}

.comment-popup textarea {
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 8px;
  font-size: 14px;
  resize: none;
}

.comment-popup-buttons {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  justify-content: flex-end;
}

.comment-popup-buttons button {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
}

.comment-popup-buttons button:last-child {
  background: var(--color-primary);
  color: white;
}
</style>