
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { UserPreference, type UserPreferenceJson } from "./model";
import { userPreferenceSchema } from "./schema";


const ENDPOINT = "/user-preference";
const TABLE = "user_preference";
const PK = "id";

export const userPreferenceRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: UserPreference): Promise<UserPreference> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, userPreferenceSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return UserPreference.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => UserPreference.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<UserPreference> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, userPreferenceSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return UserPreference.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => UserPreference.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<UserPreference>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, userPreferenceSchema);
      const items = db.getAll(TABLE).map(UserPreference.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => UserPreference.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<UserPreference>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, userPreferenceSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(UserPreference.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => UserPreference.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<UserPreferenceJson>,
  ): Promise<UserPreference> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, userPreferenceSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return UserPreference.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => UserPreference.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, userPreferenceSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
