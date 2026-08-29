
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { Datatypestest, type DatatypestestJson } from "./model";
import { datatypestestSchema } from "./schema";


const ENDPOINT = "/datatypestest";
const TABLE = "datatypestest";
const PK = "keykey";

export const datatypestestRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: Datatypestest): Promise<Datatypestest> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, datatypestestSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return Datatypestest.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => Datatypestest.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getByKeykey(keykey: number): Promise<Datatypestest> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, datatypestestSchema);
      const row = db.getById(TABLE, PK, keykey);
      if (!row) throw new ApiException("Not found", 404);
      return Datatypestest.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ keykey }`, {
      fromJson: (json) => Datatypestest.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<Datatypestest>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, datatypestestSchema);
      const items = db.getAll(TABLE).map(Datatypestest.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => Datatypestest.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<Datatypestest>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, datatypestestSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(Datatypestest.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(`${ENDPOINT}/search`, {
      params: { ...filters, ...pagination },
      fromJson: (json) => Datatypestest.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateByKeykey(
    keykey: number,
    updates: Partial<DatatypestestJson>,
  ): Promise<Datatypestest> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, datatypestestSchema);
      const updated = db.update(TABLE, PK, keykey, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return Datatypestest.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ keykey }`, {
      data: updates,
      fromJson: (json) => Datatypestest.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteByKeykey(keykey: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, datatypestestSchema);
      db.remove(TABLE, PK, keykey);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ keykey }`);
  },
};
