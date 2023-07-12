import { Notify } from 'quasar';
import { timeTableData } from './PersistanceDB.hooks';
import { computed, ref } from 'vue';

export const defaultGroup = [
  'C111',
  'C112',
  'C113',
  'C121',
  'C122',
  'C211',
  'C212',
  'C213',
  'C311',
  'C312',
  'C411',
  'C412',
  'M1',
  'M2',
  'M3',
  'M4',
  'CD1',
];
export const defaultYear = ['2023', 'test'];

export const emptyTimeState = ['1', '2', '3', 'Receso', '4', '5', '6'].map(
  (v) => {
    return {
      turn: ` ${v} `,
      monday: '',
      tuesday: '',
      wednesday: '',
      thursday: '',
      friday: '',
    };
  }
);

const emptySchoolState = ['1', '2', '3', '4', '5', '6', '7', '8', '9'].map(
  (v) => {
    return {
      turn: `[ ${v} ]`,
      monday: '',
      tuesday: '',
      wednesday: '',
      thursday: '',
      friday: '',
    };
  }
);

export const defaultTimeTablingObject = defaultGroup.reduce(
  (prev, current) => ({
    ...prev,
    [current]: emptyTimeState,
  }),
  {}
);

export const defaultTimeTablingYearObject = defaultYear.reduce(
  (prev, current) => ({
    ...prev,
    [current]: {
      groups: defaultTimeTablingObject,
      rooms: emptySchoolState,
    },
  }),
  {}
);

export const useTimetabling = () => {
  const { loadData: timeLoad, saveData: timeSave } = timeTableData;

  const groupData = ref(timeLoad() || defaultTimeTablingYearObject);

  const yearKeys = computed(() => {
    return Object.keys(groupData.value);
  });

  const groupKeys = computed(() => {
    return Object.keys(groupData.value[selectedYear.value].groups);
  });
  const selectedYear = ref(yearKeys.value[0]);
  const selectedGroup = ref(groupKeys.value[0]);

  const addYear = (year: string) => {
    groupData.value[year] = {
      groups: defaultTimeTablingObject,
      rooms: emptySchoolState,
    };
    timeSave(groupData.value);
    selectedYear.value = year;
    selectedGroup.value = groupKeys.value[0];
    Notify.create({
      type: 'positive',
      message: `El horario ${year} fue creado y salvado correctamente`,
    });
  };

  const addGroup = (group: string) => {
    groupData.value[selectedYear.value].groups[group] = emptyTimeState;
    timeSave(groupData.value);
    selectedGroup.value = group;
  };

  return {
    groupData,
    groupKeys,
    yearKeys,
    selectedYear,
    selectedGroup,
    addGroup,
    addYear,
    onChangeYear(year: string) {
      selectedYear.value = year;
      if (
        !Object.keys(groupData.value[year].groups).includes(selectedGroup.value)
      ) {
        selectedGroup.value = Object.keys(groupData.value[year].groups)[0];
      }
    },
    onSave() {
      timeSave(groupData.value);
    },
    onClear() {
      // groupData.value[selectedYear.value].groups[selectedGroup.value] =
      //   emptyTimeState;
      // groupData.value[selectedYear.value].rooms = emptySchoolState;
      groupData.value = defaultTimeTablingYearObject;
      timeSave(groupData.value);
    },
  };
};