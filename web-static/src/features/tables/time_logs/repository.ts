
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { TimeLog, type TimeLogJson } from "./model";
import { time_logsSchema } from "./schema";


const ENDPOINT = "/time-logs";
const TABLE = "time_logs";
const PK = "timeLogId";

export const time_logsRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: TimeLog): Promise<TimeLog> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, time_logsSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return TimeLog.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => TimeLog.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<TimeLog> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, time_logsSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return TimeLog.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => TimeLog.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<TimeLog>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, time_logsSchema);
      const items = db.getAll(TABLE).map(TimeLog.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => TimeLog.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<TimeLog>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, time_logsSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(TimeLog.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(`${ENDPOINT}/search`, {
      params: { ...filters, ...pagination },
      fromJson: (json) => TimeLog.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<TimeLogJson>,
  ): Promise<TimeLog> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, time_logsSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return TimeLog.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => TimeLog.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, time_logsSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
