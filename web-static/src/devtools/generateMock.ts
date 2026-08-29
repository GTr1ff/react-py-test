import { Column } from '@/types/column';
import { Table } from '@/types/table';
import { faker } from '@faker-js/faker';

type CellValue = string | number | boolean | null;
type Row = Record<string, CellValue>;

const NAME_HEURISTICS: Array<[RegExp, () => string]> = [
  // People
  [/name/, () => faker.person.fullName()],
  [/first_name|given_name/, () => faker.person.firstName()],
  [/last_name|surname|family_name/, () => faker.person.lastName()],
  [/middle_name/, () => faker.person.middleName()],
  [/full_name/, () => faker.person.fullName()],
  [/username|user_name|^login$/, () => faker.internet.username()],
  [/password/, () => faker.internet.password()],
  [/job_title|^title$|position/, () => faker.person.jobTitle()],
  [/gender|sex/, () => faker.person.sex()],

  // Contact
  [/email/, () => faker.internet.email()],
  [/phone|mobile|fax/, () => faker.phone.number()],
  [/url|website|homepage/, () => faker.internet.url()],
  [/domain/, () => faker.internet.domainName()],
  [/ip_address|^ip$/, () => faker.internet.ip()],
  [/mac_address/, () => faker.internet.mac()],
  [/user_agent/, () => faker.internet.userAgent()],

  // Location
  [/location/, () => faker.location.streetAddress()],
  [/street|^address$|address_line/, () => faker.location.streetAddress()],
  [/city/, () => faker.location.city()],
  [/state|province/, () => faker.location.state()],
  [/country/, () => faker.location.country()],
  [/zip|postal_code|postcode/, () => faker.location.zipCode()],
  [/latitude|^lat$/, () => String(faker.location.latitude())],
  [/longitude|^lng$|^lon$/, () => String(faker.location.longitude())],
  [/timezone/, () => faker.location.timeZone()],

  // Company/commerce
  [/company|organi[sz]ation|employer/, () => faker.company.name()],
  [/department/, () => faker.commerce.department()],
  [/product/, () => faker.commerce.productName()],
  [/sku/, () => faker.string.alphanumeric(8).toUpperCase()],
  [/currency_code|^currency$/, () => faker.finance.currencyCode()],
  [/iban/, () => faker.finance.iban()],
  [/account_number/, () => faker.finance.accountNumber()],
  [/credit_card/, () => faker.finance.creditCardNumber()],
  [/bitcoin|btc_address/, () => faker.finance.bitcoinAddress()],

  // Identifiers
  [/^uuid$|_uuid$|^guid$/, () => faker.string.uuid()],
  [/^slug$|_slug$/, () => faker.lorem.slug()],
  [/^token$|_token$|api_key/, () => faker.string.alphanumeric(32)],
  [/^colou?r$|hex_colou?r/, () => faker.color.rgb()],

  // Content
  [/^description$|_description$/, () => faker.lorem.sentence()],
  [/^comment$|_comment$|^note$|_notes$/, () => faker.lorem.paragraph()],
  [/^bio$|^biography$|^about$/, () => faker.person.bio()],
  [/^tags?$|^category$/, () => faker.lorem.word()],
  [/^language$|^locale$/, () => faker.location.countryCode()],

  // Status/type enums
  [/^status$/, () => faker.helpers.arrayElement(['active', 'inactive', 'pending', 'archived'])],
  [/^type$|_type$/, () => faker.helpers.arrayElement(['standard', 'premium', 'basic'])],
  [/^role$/, () => faker.helpers.arrayElement(['admin', 'user', 'guest', 'moderator'])],
];

function generateValue(column: Column): CellValue {
  if (column.isNullable && Math.random() < 0.1) return null;

  const type = column.dataType.toLowerCase();

  if (type === 'date') {
    return faker.date.past().toISOString().split('T')[0];
  }
  if (type.includes('timestamp') || type === 'datetime') {
    return faker.date.past().toISOString();
  }
  if (type === 'time' || type === 'time without time zone' || type === 'time with time zone') {
    return faker.date.past().toISOString().split('T')[1].split('.')[0];
  }
  if (
    type === 'integer' ||
    type === 'int' ||
    type === 'bigint' ||
    type === 'smallint' ||
    type === 'serial' ||
    type === 'bigserial'
  ) {
    if (column.isAutoIncrement) return null;
    return faker.number.int({ min: 0, max: 10000 });
  }
  if (
    type === 'decimal' ||
    type === 'numeric' ||
    type === 'real' ||
    type === 'double precision' ||
    type === 'float'
  ) {
    return faker.number.float({
      min: 0,
      max: 10000,
      fractionDigits: column.numericScale || 2,
    });
  }
  if (
    type === 'character varying' ||
    type === 'varchar' ||
    type === 'character' ||
    type === 'char' ||
    type === 'text' ||
    type === 'string'
  ) {
    return generateString(column);
  }
  if (type === 'boolean' || type === 'bool') {
    return faker.datatype.boolean();
  }
  if (type === 'uuid') {
    return faker.string.uuid();
  }
  if (type === 'json' || type === 'jsonb') {
    return JSON.stringify({ key: faker.lorem.word() });
  }

  return null;
}

function generateString(column: Column): string {
  const columnName = column.name.toLowerCase();

  for (const [pattern, generator] of NAME_HEURISTICS) {
    if (pattern.test(columnName)) {
      return generator();
    }
  }

  // Fallback
  const max = column.maxLength || 50;
  return faker.lorem.words(3).slice(0, max);
}

function toCamelCase(s: string): string {
  return s.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
}

function generateRow(table: Table, rowIndex: number): Row {
  const row: Row = {};
  for (const column of table.columns) {
    const key = toCamelCase(column.name);
    row[key] = column.isAutoIncrement ? rowIndex + 1 : generateValue(column);
  }
  return row;
}

export function generateRows(table: Table, count = 10): Row[] {
  return Array.from({ length: count }, (_, i) => generateRow(table, i));
}