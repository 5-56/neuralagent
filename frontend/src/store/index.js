// Redux store配置（如果需要的话）
import { configureStore } from '@reduxjs/toolkit';

// 这里可以添加Redux slices
const store = configureStore({
  reducer: {
    // 添加reducers
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export { store };