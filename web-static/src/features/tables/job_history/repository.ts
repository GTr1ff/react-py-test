
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { JobHistory, type JobHistoryJson } from "./model";
import { job_historySchema } from "./schema";


const ENDPOINT = "/job-history";
const TABLE = "job_history";
const PK = "jobHistoryId";

export const job_historyRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: JobHistory): Promise<JobHistory> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, job_historySchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return JobHistory.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => JobHistory.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<JobHistory> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, job_historySchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return JobHistory.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => JobHistory.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<JobHistory>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, job_historySchema);
      const items = db.getAll(TABLE).map(JobHistory.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => JobHistory.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<JobHistory>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, job_historySchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(JobHistory.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(`${ENDPOINT}/search`, {
      params: { ...filters, ...pagination },
      fromJson: (json) => JobHistory.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<JobHistoryJson>,
  ): Promise<JobHistory> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, job_historySchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return JobHistory.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => JobHistory.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, job_historySchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
