
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { Notification, type NotificationJson } from "./model";
import { notificationSchema } from "./schema";


const ENDPOINT = "/notification";
const TABLE = "notification";
const PK = "id";

export const notificationRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: Notification): Promise<Notification> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, notificationSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return Notification.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => Notification.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<Notification> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, notificationSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return Notification.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => Notification.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<Notification>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, notificationSchema);
      const items = db.getAll(TABLE).map(Notification.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => Notification.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<Notification>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, notificationSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(Notification.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => Notification.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<NotificationJson>,
  ): Promise<Notification> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, notificationSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return Notification.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => Notification.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, notificationSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
