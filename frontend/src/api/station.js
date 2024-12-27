import { reqApi } from "./base";

const PREFIX = "/station/";

export const addStation = async (data) => {
  return (await reqApi(`${PREFIX}add/`, data, "POST")).data;
};

export const getStations = async () => {
  return (await reqApi(PREFIX)).data;
};

export const getStationsParams = async (start_date=null, end_date=null) => {
  const filters = {}
  if (start_date) filters.start_date = start_date;
  if (end_date) filters.end_date = end_date;
  return (await reqApi(PREFIX,
    filters
  )).data;
};

export const getStation = async (station=null, start_date=null, end_date=null) => {
  const filters = {}
  if (station) filters.station = station;
  if (start_date) filters.start_date = start_date;
  if (end_date) filters.end_date = end_date;
  return (await reqApi(PREFIX,
    filters
  )).data;
};

export const getParameterNames = async () => {
  return (await reqApi(`/parameter-names`)).data;
};

export const getParameter = async (station_id) => {
  return (await reqApi(`/station/parameter`, {station: station_id})).data;
};