import { IHost } from "../IHost"

export interface ClusterData {
    action_vars: any
    actions: Action[]
    extid: string
    files_vars: any
    hosts: IHostCluster[]
    name: string
    requirements_groups: RequirementsGroup[]
    vars_service: VarsService[]
}

interface IHostCluster extends IHost {
    group: string | null
}

interface Action {
    extid: string
    name: string
    params: any
    shell: string 
}

interface VarsService {
    description: string[]
    extid: string
    file: any
    type: string
}

interface RequirementsGroup {
    count: number
    quantity_max: number
    type_host: string
}