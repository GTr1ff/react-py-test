
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { Consent, type ConsentJson } from "./model";
import { consentSchema } from "./schema";


const ENDPOINT = "/consent";
const TABLE = "consent";
const PK = "id";

export const consentRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: Consent): Promise<Consent> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, consentSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return Consent.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => Consent.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<Consent> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, consentSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return Consent.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => Consent.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<Consent>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, consentSchema);
      const items = db.getAll(TABLE).map(Consent.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => Consent.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<Consent>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, consentSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(Consent.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => Consent.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<ConsentJson>,
  ): Promise<Consent> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, consentSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return Consent.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => Consent.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, consentSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
