export interface BasePalletteSetter {
  readonly name: string;
  type: 'light' | 'dark';
  setColorPallette: () => void;
}
