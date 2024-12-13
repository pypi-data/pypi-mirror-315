import type { IDataSourceProps } from "../interfaces";
import type { IRow, IDataQueryPayload, IChart } from "@kanaries/graphic-walker/interfaces";
interface ICommPostDataMessage {
    dataSourceId: string;
    data?: IRow[];
    total: number;
    curIndex: number;
}
export declare function loadDataSource(props: IDataSourceProps): Promise<IRow[]>;
export declare function postDataService(msg: ICommPostDataMessage): void;
export declare function finishDataService(msg: any): void;
export declare function getDatasFromKernelBySql(fieldMetas: any): (payload: IDataQueryPayload) => Promise<IRow[]>;
export declare function getDatasFromKernelByPayload(payload: IDataQueryPayload): Promise<IRow[]>;
export declare function getImageFromKernelBySpec(spec: IChart, size: {
    width: number;
    height: number;
}, workflow: IDataQueryPayload): Promise<any>;
export declare function getCodesFromKernelBySpec(spec: IChart): Promise<any>;
export {};
