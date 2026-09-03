
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { AuditLog, type AuditLogJson } from "./model";
import { auditLogSchema } from "./schema";


const ENDPOINT = "/audit-log";
const TABLE = "audit_log";
const PK = "id";

export const auditLogRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: AuditLog): Promise<AuditLog> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, auditLogSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return AuditLog.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => AuditLog.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<AuditLog> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, auditLogSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return AuditLog.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => AuditLog.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<AuditLog>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, auditLogSchema);
      const items = db.getAll(TABLE).map(AuditLog.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => AuditLog.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<AuditLog>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, auditLogSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(AuditLog.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.postPaginated(`${ENDPOINT}/search`, {
      data: filters,
      params: pagination,
      fromJson: (json) => AuditLog.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<AuditLogJson>,
  ): Promise<AuditLog> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, auditLogSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return AuditLog.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => AuditLog.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, auditLogSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
