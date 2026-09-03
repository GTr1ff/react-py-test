import { create } from "zustand";
import { generateRows } from "@/devtools/generateMock";
import { type Table } from "@/types/table";

interface Row {
  [key: string]: unknown;
}

interface MockDbState {
  tables: Record<string, Row[]>;
  seed: (tableName: string, schema: Table) => void;
  getAll: (tableName: string) => Row[];
  getById: (tableName: string, pk: string, id: unknown) => Row | undefined;
  insert: (tableName: string, row: Row, pkField: string) => Row;
  update: (tableName: string, pk: string, id: unknown, updates: Row) => Row | undefined;
  remove: (tableName: string, pk: string, id: unknown) => boolean;
}

export const useMockDb = create<MockDbState>((set, get) => ({
  tables: {},

  seed: (tableName, schema) => {
    if (get().tables[tableName]) return;
    set((s) => ({ tables: { ...s.tables, [tableName]: generateRows(schema, 10) } }));
  },

  getAll: (tableName) => get().tables[tableName] ?? [],

  getById: (tableName, pk, id) =>
    (get().tables[tableName] ?? []).find((r) => r[pk] === id),

  insert: (tableName, row, pkField) => {
    const rows = get().tables[tableName] ?? [];
    const nextId = rows.reduce((max, r) => Math.max(max, Number(r[pkField]) || 0), 0) + 1;
    const withId = { ...row, [pkField]: nextId };
    set((s) => ({ tables: { ...s.tables, [tableName]: [...rows, withId] } }));
    return withId;
  },

  update: (tableName, pk, id, updates) => {
    const rows = get().tables[tableName] ?? [];
    const idx = rows.findIndex((r) => r[pk] === id);
    if (idx === -1) return undefined;
    const updated = { ...rows[idx], ...updates };
    const next = [...rows];
    next[idx] = updated;
    set((s) => ({ tables: { ...s.tables, [tableName]: next } }));
    return updated;
  },

  remove: (tableName, pk, id) => {
    const rows = get().tables[tableName] ?? [];
    const next = rows.filter((r) => r[pk] !== id);
    if (next.length === rows.length) return false;
    set((s) => ({ tables: { ...s.tables, [tableName]: next } }));
    return true;
  },
}));