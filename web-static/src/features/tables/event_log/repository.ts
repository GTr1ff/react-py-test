
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { EventLog, type EventLogJson } from "./model";
import { eventLogSchema } from "./schema";


const ENDPOINT = "/event-log";
const TABLE = "event_log";
const PK = "id";

export const eventLogRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: EventLog): Promise<EventLog> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, eventLogSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return EventLog.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => EventLog.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<EventLog> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, eventLogSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return EventLog.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => EventLog.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<EventLog>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, eventLogSchema);
      const items = db.getAll(TABLE).map(EventLog.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => EventLog.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<EventLog>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, eventLogSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(EventLog.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => EventLog.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<EventLogJson>,
  ): Promise<EventLog> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, eventLogSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return EventLog.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => EventLog.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, eventLogSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
