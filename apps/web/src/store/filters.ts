import { create } from "zustand";

type FiltersState = {
  category: string | null;
  setCategory: (c: string | null) => void;
};

export const useFilters = create<FiltersState>((set) => ({
  category: null,
  setCategory: (category) => set({ category }),
}));
