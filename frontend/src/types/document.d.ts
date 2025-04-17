export interface Document {
    name: string;
    description: string;
    tags?: string[];
    university: string;
    dType: string;
    versions: Version[]
}